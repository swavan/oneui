pyinstaller SwaVanOneUI.py --onedir --noconfirm --windowed \
--name "SwaVan" \
--icon='assets/images/logo/swavan_one_ui.icns' \
--add-data "assets:assets" \
--add-data "data:data" \
--add-data "mock/servers/rest/certs:mock/servers/rest/certs" \
--hidden-import "PyQt6.sip" \
--clean
