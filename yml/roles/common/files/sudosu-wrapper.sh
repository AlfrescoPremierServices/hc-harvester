#!/bin/bash

more_sudo_opts=''

while getopts :u:p:HS options; do
	case $options in
		u) become_user=$OPTARG
		;;
		p) sudo_prompt="$OPTARG"
		;;
		H) more_sudo_opts="$more_sudo_opts -H"
		;;
	esac
done

shift $(($OPTIND-1))
for i in "$@"; do 
    i="${i//\\/\\\\}"
    become_cmd="$become_cmd \"${i//\"/\\\"}\""
done

user_shell=$(getent passwd $become_user | cut -d : -f 7)
current_user_shell=$(getent passwd `whoami` | cut -d : -f 7)
[ x${user_shell##*/} == xfalse -o x${user_shell##*/} == xnologin ] && su_opts="-s $current_user_shell"

if [ -n "$sudo_prompt" ]; then
  sudo $more_sudo_opts -p "$sudo_prompt" su $su_opts - $become_user << END
$become_cmd
END
else sudo $more_sudo_opts su $su_opts - $become_user << END
$become_cmd
END
fi
