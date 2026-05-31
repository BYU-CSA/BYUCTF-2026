# Gitastic 4
Description:
```markdown
Walker reported that he accidentally pushed an API key to our public repo. Luckily he deleted it afterward so we're completed safe and secure!

git clone git://gitastic.csa.cyberjousting.com/challenge
```
**Author**: `Zinko`
## Writeup
Players need to find the deleted file and read it. There's a great article on geeksforgeeks about this.

They can run `git log --diff-filter=D --summary` to find the files that were deleted. They can
They find the apikey.txt was deleted in commit `f3361dcede9b2337bbbf51ff08d6fbb215186bbd`.

Next, checkout the commit right before it was deleted `git checkout f3361dcede9b2337bbbf51ff08d6fbb215186bbd~1`.

Finally, `cat apikey.txt`.

**Flag** - `byuctf{But_th3s_was_d3l3t3d?}`
