#!/bin/bash
set -x
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

if [ -n "$sudo_prompt" ]; then
  sudo $more_sudo_opts -p "$sudo_prompt" su - $become_user << END
$become_cmd
END
else sudo $more_sudo_opts su - $become_user << END
$become_cmd
END
fi
