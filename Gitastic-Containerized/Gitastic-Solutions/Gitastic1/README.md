# Gitastic 1
Description:
```markdown
We've recently found out that one of our employees has been exfiltrating information to a competitor. They did it via messages attached to each code change he made. Find the secret that was exfiltrated!

git clone git://gitastic.csa.cyberjousting.com/challenge
```
**Author**: `Zinko`
## Writeup
Players are supposed to deduce that "messages attached to each code change" means a commit message. They then need to figure out how to search the commit history.

They can run `git log --grep byu` to find the flag.

**Flag** - `byuctf{I_hop3_y0u_didnt_s3@rch_manually}`
