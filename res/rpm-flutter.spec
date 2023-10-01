Name:       OABRemoteDesk
Version:    1.2.3
Release:    0
Summary:    RPM package
License:    GPL-3.0
Requires:   gtk3 libxcb libxdo libXfixes alsa-lib libappindicator-gtk3 libvdpau libva pam gstreamer1-plugins-base
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/lib/OABRemoteDesk" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/lib/OABRemoteDesk"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/OABRemoteDesk.service -t "%{buildroot}/usr/share/OABRemoteDesk/files"
install -Dm 644 $HBB/res/OABRemoteDesk.desktop -t "%{buildroot}/usr/share/OABRemoteDesk/files"
install -Dm 644 $HBB/res/OABRemoteDesk-link.desktop -t "%{buildroot}/usr/share/OABRemoteDesk/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/OABRemoteDesk.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/OABRemoteDesk.svg"

%files
/usr/lib/OABRemoteDesk/*
/usr/share/OABRemoteDesk/files/OABRemoteDesk.service
/usr/share/icons/hicolor/256x256/apps/OABRemoteDesk.png
/usr/share/icons/hicolor/scalable/apps/OABRemoteDesk.svg
/usr/share/OABRemoteDesk/files/OABRemoteDesk.desktop
/usr/share/OABRemoteDesk/files/OABRemoteDesk-link.desktop

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
ln -s /usr/lib/OABRemoteDesk/OABRemoteDesk /usr/bin/OABRemoteDesk
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
    rm /usr/bin/OABRemoteDesk || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
