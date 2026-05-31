from flask import Flask, request, render_template_string, make_response
import html

app = Flask(__name__)

ADMIN_COOKIE_NAME = "admin_pass"
ADMIN_PASSWORD = "super_secret_admin_password_999_lol"
FLAG = "byuctf{s33_1t5_3asy!}"
HOST = "0.0.0.0"
PORT = 5000

# In-memory ticket storage
tickets = []

# Shared CSS for consistent styling
BASE_STYLE = """
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 2rem;
    }
    .container {
        max-width: 900px;
        margin: 0 auto;
        background: white;
        border-radius: 1rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        padding: 2.5rem;
    }
    h1, h2 { 
        color: #2d3748;
        margin-bottom: 1.5rem;
    }
    h1 {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .button, button {
        display: inline-block;
        padding: 0.75rem 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-decoration: none;
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        font-size: 1rem;
    }
    .button:hover, button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
    }
    .links { 
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin-bottom: 1.5rem;
    }
    a.back-link {
        color: #667eea;
        text-decoration: none;
        font-weight: 600;
        margin-top: 1.5rem;
        display: inline-block;
    }
    a.back-link:hover {
        text-decoration: underline;
    }
    .info-box {
        background: #f7fafc;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin-top: 1.5rem;
        border-radius: 0.5rem;
    }
"""

@app.route("/")
def index():
    return f"""
    <html>
      <head>
        <title>Support Tickets</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
          {BASE_STYLE}
        </style>
      </head>
      <body>
        <div class="container">
          <h1>🎫 Support Ticket Portal</h1>
          <div class="links">
            <a class="button" href="/submit">Submit a Ticket</a>
            <a class="button" href="/login">Login</a>
            <a class="button" href="/tickets">View Tickets</a>
          </div>
          <div class="info-box">
            <p>📬 Submit a ticket and our admin will review it regularly.</p>
          </div>
        </div>
      </body>
    </html>
    """

@app.route("/login", methods=["GET"])
def login():
    return f"""
    <html>
      <head>
        <title>Login</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
          {BASE_STYLE}
          #out {{
            margin-top: 1rem;
            padding: 1rem;
            border-radius: 0.5rem;
            font-weight: 600;
          }}
          .ok {{
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
          }}
          .bad {{
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
          }}
          .hint {{
            color: #718096;
            font-size: 0.9rem;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <h2>🔐 Login Check</h2>
          <p class="hint" style="margin-bottom: 1.5rem;">This checks if your cookie is correct for viewing tickets.</p>
          <button onclick="check()">Check My Login Status</button>
          <div id="out"></div>
          <a href="/" class="back-link">← Back to Home</a>
        </div>
        <script>
          async function check() {{
            const r = await fetch('/whoami');
            const t = await r.text();
            const el = document.getElementById('out');
            if (t.includes('OK')) {{
              el.className = 'ok';
              el.innerHTML = '✅ Success! You can access <a href="/tickets" style="color:#155724;font-weight:bold;">tickets</a>';
            }} else {{
              el.className = 'bad';
              el.innerHTML = '❌ Invalid cookie. Set the correct cookie via DevTools (Application → Cookies).';
            }}
          }}
        </script>
      </body>
    </html>
    """

@app.route("/whoami")
def whoami():
    v = request.cookies.get(ADMIN_COOKIE_NAME)
    return "OK" if v == ADMIN_PASSWORD else "NOPE", (200 if v == ADMIN_PASSWORD else 403)

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "GET":
        return f"""
        <html>
          <head>
            <title>Submit Ticket</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
              {BASE_STYLE}
              form div {{ margin-bottom: 1.25rem; }}
              label {{
                display: block;
                margin-bottom: 0.5rem;
                color: #4a5568;
                font-weight: 600;
              }}
              input, textarea {{
                width: 100%;
                padding: 0.75rem;
                border: 2px solid #e2e8f0;
                border-radius: 0.5rem;
                font-size: 1rem;
                transition: border-color 0.3s ease;
              }}
              input:focus, textarea:focus {{
                outline: none;
                border-color: #667eea;
              }}
              textarea {{
                height: 150px;
                resize: vertical;
                font-family: inherit;
              }}
            </style>
          </head>
          <body>
            <div class="container">
              <h2>📝 Submit a Support Ticket</h2>
              <form method="POST">
                <div>
                  <label>Subject</label>
                  <input name="subject" autocomplete="off" placeholder="Brief description of your issue">
                </div>
                <div>
                  <label>Message</label>
                  <textarea name="message" placeholder="Detailed message..."></textarea>
                </div>
                <div>
                  <button type="submit">Submit Ticket</button>
                </div>
              </form>
              <a href="/" class="back-link">← Back to Home</a>
            </div>
          </body>
        </html>
        """
    
    # POST
    subject = request.form.get("subject", "")
    message = request.form.get("message", "")
    tid = len(tickets)
    tickets.append({"id": tid, "subject": subject, "message": message})
    
    return f"""
    <html>
      <head>
        <title>Ticket Submitted</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
          {BASE_STYLE}
          .success-box {{
            background: #d4edda;
            border: 2px solid #c3e6cb;
            color: #155724;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 1.5rem;
            text-align: center;
          }}
          .success-box strong {{
            font-size: 1.2rem;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <h2>✅ Ticket Submitted!</h2>
          <div class="success-box">
            <strong>Your Ticket ID: #{tid}</strong>
            <p style="margin-top:0.5rem;">Our admin will review your ticket soon.</p>
          </div>
          <a href="/" class="button">← Back to Home</a>
        </div>
      </body>
    </html>
    """

@app.route("/tickets")
def tickets_page():
    cookie_val = request.cookies.get(ADMIN_COOKIE_NAME)
    if cookie_val != ADMIN_PASSWORD:
        return f"""
        <html>
          <head>
            <title>Unauthorized</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
              {BASE_STYLE}
              .error-box {{
                background: #f8d7da;
                border: 2px solid #f5c6cb;
                color: #721c24;
                padding: 2rem;
                border-radius: 0.5rem;
                text-align: center;
              }}
            </style>
          </head>
          <body>
            <div class="container">
              <h2>🔒 Unauthorized</h2>
              <div class="error-box">
                <strong>Access Denied</strong>
                <p style="margin-top:0.5rem;">Missing or incorrect cookie.</p>
              </div>
              <a href="/" class="button">← Back to Home</a>
            </div>
          </body>
        </html>
        """, 403
    
    items_html = ""
    for t in tickets:
        subj = html.escape(t["subject"] or "(no subject)")
        msg = t["message"] or ""
        items_html += f"""
          <div class="ticket">
            <div class="ticket-header">
              <span class="ticket-id">#{t["id"]}</span>
              <h3>{subj}</h3>
            </div>
            <div class="ticket-body">{msg}</div>
          </div>
        """
    
    page = f"""
    <html>
      <head>
        <title>Tickets</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
          {BASE_STYLE}
          .flag {{
            background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
            padding: 1.5rem;
            border-radius: 0.75rem;
            margin-bottom: 2rem;
            border: 3px solid #fdcb6e;
            box-shadow: 0 4px 12px rgba(253, 203, 110, 0.4);
          }}
          .flag strong {{
            font-size: 1.2rem;
            color: #2d3748;
          }}
          .flag code {{
            background: white;
            padding: 0.5rem 1rem;
            border-radius: 0.25rem;
            font-family: 'Courier New', monospace;
            font-size: 1.1rem;
            color: #e74c3c;
            display: inline-block;
            margin-top: 0.5rem;
          }}
          .ticket {{
            background: #f7fafc;
            border-radius: 0.75rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid #e2e8f0;
            transition: box-shadow 0.3s ease;
          }}
          .ticket:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
          }}
          .ticket-header {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
          }}
          .ticket-id {{
            background: #667eea;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-weight: 600;
            font-size: 0.9rem;
          }}
          .ticket-header h3 {{
            margin: 0;
            color: #2d3748;
            font-size: 1.25rem;
          }}
          .ticket-body {{
            color: #4a5568;
            line-height: 1.6;
          }}
          .no-tickets {{
            text-align: center;
            padding: 3rem;
            color: #718096;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <div class="flag">
            <strong>🚩 FLAG:</strong>
            <code>{html.escape(FLAG)}</code>
          </div>
          <h2>📋 All Support Tickets</h2>
          {items_html if items_html.strip() else '<div class="no-tickets"><p>No tickets submitted yet.</p></div>'}
          <a href="/" class="back-link">← Back to Home</a>
        </div>
      </body>
    </html>
    """

    # Build the response *first*
    resp = make_response(render_template_string(page))

    # Then clear the tickets after the admin (bot) has "seen" them
    tickets.clear()

    return resp

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
