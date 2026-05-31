const puppeteer = require('puppeteer');

const ADMIN_COOKIE_NAME = "admin_pass";
const ADMIN_PASSWORD = "super_secret_admin_password_999_lol";
const TICKETS_URL = "http://127.0.0.1:5000/tickets";
const PATROL_INTERVAL = 5000; 

// Visit the tickets page with the admin cookie
const visitTickets = async () => {
    let browser;
    try {
        browser = await puppeteer.launch({
            headless: "new",
            pipe: true,
            dumpio: true,
            args: [
                '--no-sandbox',
                '--disable-gpu',
                '--disable-software-rasterizer',
                '--disable-dev-shm-usage',
                '--disable-setuid-sandbox',
                '--js-flags=--noexpose_wasm,--jitless'
            ]
        });

        const page = await browser.newPage();
        
        // Set the admin cookie before visiting the page
        await page.setCookie({
            name: ADMIN_COOKIE_NAME,
            value: ADMIN_PASSWORD,
            domain: '127.0.0.1',
            path: '/',
            httpOnly: false,
            secure: false
        });

        await page.setUserAgent('AdminBot/1.0');
        
        console.log(`[${new Date().toISOString()}] Admin bot visiting tickets page...`);
        await page.goto(TICKETS_URL, { 
            timeout: 5000, 
            waitUntil: 'networkidle2' 
        });
        
        // Wait a bit for any scripts to execute
        await page.waitForTimeout(2000);
        
        console.log(`[${new Date().toISOString()}] Admin bot finished visiting tickets page`);
        
        await page.close();
    } catch (e) {
        console.error(`[${new Date().toISOString()}] Error during admin bot visit:`, e.message);
    } finally {
        if (browser) {
            await browser.close();
        }
    }
};

// Patrol function - visits tickets page every PATROL_INTERVAL milliseconds
const startPatrol = async () => {
    console.log(`[${new Date().toISOString()}] Admin bot started patrolling every ${PATROL_INTERVAL}ms`);
    
    // Initial visit
    await visitTickets();
    
    // Set up periodic visits
    setInterval(async () => {
        await visitTickets();
    }, PATROL_INTERVAL);
};

// Start the patrol
startPatrol().catch(err => {
    console.error('Fatal error starting admin bot:', err);
    process.exit(1);
});
