use actix_files::NamedFile;
use actix_web::{App, HttpRequest, HttpResponse, HttpServer, Responder, cookie::Cookie, get, web};

use aes_gcm::{
    Aes256Gcm, Key, Nonce,
    aead::{Aead, KeyInit},
};
use sha2::{Digest, Sha256};

use base64::{Engine as _, engine::general_purpose::URL_SAFE};

use hex;
use once_cell::sync::Lazy;
use serde::{Deserialize, Serialize};
use std::time::{SystemTime, UNIX_EPOCH};
use uuid::Uuid;

static KEY: Lazy<[u8; 32]> = Lazy::new(|| {
    let key_hex = std::env::var("APP_SECRET_KEY").expect("APP_SECRET_KEY must be set");

    let mut key = [0u8; 32];
    hex::decode_to_slice(key_hex, &mut key)
        .expect("Invalid Hex key in environment! Must be 64 hex chars.");

    key
});

#[derive(Serialize, Deserialize)]
struct UserCreds {
    username: String,
    password: String,
}

#[derive(Serialize, Deserialize)]
struct User {
    id: Uuid,
    role: String,
    username: String,
}

fn gen_iv() -> Result<[u8; 12], Box<dyn std::error::Error>> {
    let timestamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs();
    let mut hasher = Sha256::new();
    hasher.update(timestamp.to_be_bytes());
    let result = hasher.finalize();
    result[..12]
        .try_into()
        .map_err(|_| "Failed to create IV".into())
}

fn make_cookie(username: &str) -> Result<String, Box<dyn std::error::Error>> {
    let key_slice: &[u8; 32] = &*KEY;
    let iv = gen_iv()?;

    let cipher = Aes256Gcm::new(Key::<Aes256Gcm>::from_slice(key_slice));
    let nonce = Nonce::from_slice(&iv);

    let user = User {
        id: Uuid::new_v4(),
        role: "user".to_string(),
        username: username.to_string(),
    };

    let plaintext = serde_json::to_vec(&user)?;
    let ciphertext = cipher
        .encrypt(nonce, plaintext.as_ref())
        .map_err(|_| "Failed to encrypt cookie")?;

    Ok(URL_SAFE.encode([iv.as_ref(), ciphertext.as_ref()].concat()))
}

fn unpack_cookie(cookie_value: &str) -> Result<Option<User>, Box<dyn std::error::Error>> {
    let key_slice: &[u8; 32] = &*KEY;
    let cipher = Aes256Gcm::new(Key::<Aes256Gcm>::from_slice(key_slice));

    let decoded = URL_SAFE
        .decode(cookie_value)
        .map_err(|_| "Failed to decode cookie")?;
    if decoded.len() < 12 {
        return Ok(None);
    }
    let (iv, ciphertext) = decoded.split_at(12);
    let nonce = Nonce::from_slice(iv);

    let decrypted = cipher
        .decrypt(nonce, ciphertext.as_ref())
        .map_err(|x| "Failed to decrypt cookie: ".to_string() + &x.to_string())?;
    let user: User =
        serde_json::from_slice(&decrypted).map_err(|_| "Failed to deserialize user")?;
    Ok(Some(user))
}

#[get("/")]
async fn index(req: HttpRequest) -> impl Responder {
    if let Some(cookie) = req.cookie("session") {
        let value = cookie.value();

        let user = match unpack_cookie(value) {
            Ok(Some(u)) => u,
            Ok(None) => {
                return HttpResponse::BadRequest()
                    .content_type("text/html")
                    .body(include_str!("static/error.html"));
            }
            Err(_) => {
                return HttpResponse::InternalServerError()
                    .content_type("text/html")
                    .body(include_str!("static/error.html"));
            }
        };

        let file_path = match user.role.as_str() {
            "admin" => "src/static/admin.html",
            _ => "src/static/index.html",
        };

        match NamedFile::open(file_path) {
            Ok(file) => file
                .into_response(&req)
                .customize()
                .insert_header(("X-User-ID", user.id.to_string()))
                .respond_to(&req)
                .map_into_boxed_body(),
            Err(_) => HttpResponse::NotFound()
                .finish()
                .respond_to(&req)
                .map_into_boxed_body(),
        }
    } else {
        match NamedFile::open("src/static/login.html") {
            Ok(file) => file
                .into_response(&req)
                .respond_to(&req)
                .map_into_boxed_body(),
            Err(_) => HttpResponse::NotFound()
                .finish()
                .respond_to(&req)
                .map_into_boxed_body(),
        }
    }
}

#[get("/login")]
async fn login() -> actix_web::Result<NamedFile> {
    Ok(NamedFile::open("src/static/login.html")?)
}

#[get("/register")]
async fn register() -> actix_web::Result<NamedFile> {
    Ok(NamedFile::open("src/static/register.html")?)
}

async fn login_api(form: web::Form<UserCreds>) -> impl Responder {
    let creds = form.into_inner();

    let cookie_value = match make_cookie(&creds.username) {
        Ok(val) => val,
        Err(_) => return HttpResponse::InternalServerError().body("Failed to create cookie"),
    };
    let cookie = Cookie::build("session", cookie_value)
        .path("/")
        .secure(false)
        .http_only(true)
        .finish();

    let mut response = HttpResponse::Found()
        .append_header(("Location", "/"))
        .finish();

    response.add_cookie(&cookie).unwrap();

    response
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .service(index)
            .service(login)
            .service(register)
            .route("/api/login", web::post().to(login_api))
            .route("/api/register", web::post().to(login_api))
    })
    .bind(("0.0.0.0", 8080))?
    .run()
    .await
}
