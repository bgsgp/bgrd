; Inno Setup 脚本 - 丐点名将·队列（WPF 版本）安装程序

#define MyAppName "丐点名将·队列"
#define MyAppVersion "2.4"
#define MyAppPublisher "丐帮集团第一院·物理版象棋开发与研究院™"
#define MyAppURL "https://bgsgp.github.io/bgrd"
#define MyAppExeName "bgrd.exe"
#define MyAppIcon "D:\bgsgp\bgrd\Assets\dec.ico"

[Setup]
AppId={{644266E3-A6B2-4DE1-9B29-0BB333EEFED0}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\bggp\1\bgrd
UninstallDisplayIcon={app}\{#MyAppExeName}
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
DisableDirPage=no
DefaultGroupName=丐帮软件
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=C:\Users\LJL\Desktop
OutputBaseFilename=bgrd-wpf_v2.4_Setup
SetupIconFile={#MyAppIcon}
SolidCompression=yes
WizardStyle=modern windows11 dynamic
UsePreviousTasks=yes

[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Default.isl"
Name: "chinesetraditional"; MessagesFile: "compiler:Languages\ChineseTraditional.isl"
Name: "english"; MessagesFile: "compiler:Languages\English.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\LJL\Desktop\a\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\丐帮软件\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autoprograms}\丐帮软件\{#MyAppName} 官网"; Filename: "{#MyAppURL}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent