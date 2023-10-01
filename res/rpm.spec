Name:       OABRemoteDesk
Version:    1.2.3
Release:    0
Summary:    RPM package
License:    GPL-3.0
Requires:   gtk3 libxcb libxdo libXfixes alsa-lib libappindicator libvdpau1 libva2 pam gstreamer1-plugins-base

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/lib/OABRemoteDesk/
mkdir -p %{buildroot}/usr/share/OABRemoteDesk/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/OABRemoteDesk %{buildroot}/usr/bin/OABRemoteDesk
install $HBB/libsciter-gtk.so %{buildroot}/usr/lib/OABRemoteDesk/libsciter-gtk.so
install $HBB/res/OABRemoteDesk.service %{buildroot}/usr/share/OABRemoteDesk/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/OABRemoteDesk.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/OABRemoteDesk.svg
install $HBB/res/OABRemoteDesk.desktop %{buildroot}/usr/share/OABRemoteDesk/files/
install $HBB/res/OABRemoteDesk-link.desktop %{buildroot}/usr/share/OABRemoteDesk/files/

%files
/usr/bin/OABRemoteDesk
/usr/lib/OABRemoteDesk/libsciter-gtk.so
/usr/share/OABRemoteDesk/files/OABRemoteDesk.service
/usr/share/icons/hicolor/256x256/apps/OABRemoteDesk.png
/usr/share/icons/hicolor/scalable/apps/OABRemoteDesk.svg
/usr/share/OABRemoteDesk/files/OABRemoteDesk.desktop
/usr/share/OABRemoteDesk/files/OABRemoteDesk-link.desktop
/usr/share/OABRemoteDesk/files/__pycache__/*

%changelog
# let's skip this for now

# https://www.cnblogs.com/xingmuxin/p/8990255.html
%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop OABRemoteDesk || true
  ;;
esac

%post
cp /usr/share/OABRemoteDesk/files/OABRemoteDesk.service /etc/systemd/system/OABRemoteDesk.service
cp /usr/share/OABRemoteDesk/files/OABRemoteDesk.desktop /usr/share/applications/
cp /usr/share/OABRemoteDesk/files/OABRemoteDesk-link.desktop /usr/share/applications/
systemctl daemon-reload
systemctl enable OABRemoteDesk
systemctl start OABRemoteDesk
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop OABRemoteDesk || true
    systemctl disable OABRemoteDesk || true
    rm /etc/systemd/system/OABRemoteDesk.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/OABRemoteDesk.desktop || true
    rm /usr/share/applications/OABRemoteDesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
