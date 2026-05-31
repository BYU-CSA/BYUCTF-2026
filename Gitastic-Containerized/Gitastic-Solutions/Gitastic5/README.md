# Gitastic 5
Description:
```markdown
We're certain that someone critical info in the secrets.txt file yet we can't see anything. It's like someone has replaced it with something else! We need you to get to the bottom of this mysterious case

git clone git://gitastic.csa.cyberjousting.com/challenge
```
**Author**: `Zinko`
## Writeup
This is the hardest challenge of the gitastic series.

1) Run `git log` to find the hash of the first commit is `f88c2adbe25705ad54cabfd0c84826235446ffd0`.

2) They will also find in the commit message a message talking about checking if something has replaced it.

3) Run `git fetch origin 'refs/replace/*:refs/replace/*'`. If they then run git log again they'll notice that the log has changed to say 'replaced' on the commit at the top.

4) If they run `git show-ref` it'll show them replace refs at the top of the output. They're able to see the hash of the last commit.

5) From the last command they can see that there's a tie to the hash of their current git commit. This gives them the hash of `b82f2081365d48f0366d22c07d40b2ae8279de0c`.

6)They can run `git --no-replace-objects show b82f2081365d48f0366d22c07d40b2ae8279de0c` to see what hidden file is actually there.


**Flag** - `byuctf{I_lov3_s3cr3t_files}`
