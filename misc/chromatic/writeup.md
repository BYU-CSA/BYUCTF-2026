Ok, so this challenge is actually kinda fun in my opinion. It's a real way that I have sent data to other people, and figured I'd give up the ghost. 

At first, the challenge looks like a video of shades of red. Well, it is. However, you might notice that each shade has exactly 30 frames of video time. The only real data to be seen here are the frames themselves. Looking at each frame using something like LSB or similar will not return any data. Each frame is a single color. But, the colors codes are all interesting. Each color is a color code that only has a value for red (i.e. #620000 or #780000). 

By taking the color code from each 30 frame section, you can find the pattern with a little work. By taking the red value of each color code, and mapping it's hex value to an ASCII character, you can spell out a message. Automate it. Please. Doing this across all 54 seconds of the video reconstructs the flag character by character.

Flag: byuctf{It's_all_red_I_really_thought_it_would_be_more}

