
dependencies="rename csvkit dos2unix"

for package in $dependencies; do
	echo "Installing $package"
	sudo apt install $package
done

