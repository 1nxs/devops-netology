#!/bin/bash
# display command line options

count=1
for param in "$@"; do
<<<<<<< HEAD
=======
    echo "Next parameter: $param"
>>>>>>> 98eb8b1 (git-rebase 2)
    count=$(( $count + 1 ))
done

echo "====="
