
dependencies="rename csvkit"

for package in $dependencies; do
	echo "Installing $package"
	sudo apt install $package
done

