# Hack to customize ssh command prompt based on environment
ssh() {
    # Production: add "(PRODUCTION)" and set foreground colour to red
    if [[ $1 == prod* ]]; then
        command ssh "$@" -t "export PS1='\[\e[1;38;5;196m\][\u@\h (PRODUCTION) \W]\$ \[\e[0m\]'; bash --login"
    # QA: add "(QA)" and set foreground colour to yellow
    elif [[ $1 == qa* ]]; then
        command ssh "$@" -t "export PS1='\[\e[1;38;5;226m\][\u@\h (QA) \W]\$ \[\e[0m\]'; bash --login"
    else
        command ssh "$@"
    fi
}
