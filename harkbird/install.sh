#!/bin/bash
scriptdir=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)
shortcutpath=$HOME/.local/share/applications/HARKBird.desktop
if [ -e $HOME/デスクトップ ]; then
	deskdir=$HOME/デスクトップ
else
	deskdir=$HOME/Desktop
fi

cat > $shortcutpath <<EOF
[Desktop Entry]
Type=Application
Name=HARKBird
Terminal=false
Exec=python ${scriptdir}/harkbird
EOF

chmod +x $shortcutpath
cp $shortcutpath $deskdir
