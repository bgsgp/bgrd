; Inno Setup 脚本 - 丐点名将安装程序

#define MyAppName "丐点名将"
#define MyAppVersion "5.3"
#define MyAppPublisher "丐帮集团第一院·物理版象棋开发与研究院™"
#define MyAppURL "https://bgsgp.github.io/bgrd"
#define MyAppExeName "main.exe"
#define MyAppIcon "C:\Users\鸿合HiteVision\OneDrive\桌面\a\dec.ico"

[Setup]
AppId={{644266E3-A6B2-4DE1-9B29-0BB333EEFED0}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName=D:\Program Files\bggp\1\bgrd
UninstallDisplayIcon={app}\{#MyAppExeName}
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
DisableDirPage=no
DefaultGroupName=丐帮软件
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=C:\Users\鸿合HiteVision\OneDrive\桌面
OutputBaseFilename=bgrd_v5.3_Core_Setup
SetupIconFile={#MyAppIcon}
SolidCompression=yes
WizardStyle=modern dynamic windows11

[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Default.isl"
Name: "chinesetraditional"; MessagesFile: "compiler:Languages\ChineseTraditional.isl"
Name: "english"; MessagesFile: "compiler:Languages\English.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\鸿合HiteVision\OneDrive\桌面\a\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\丐帮软件\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autoprograms}\丐帮软件\{#MyAppName} 官网"; Filename: "{#MyAppURL}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent