{ pkgs }: {
  deps = [
    pkgs.python310
    pkgs.python310Packages.fastapi
    pkgs.python310Packages.uvicorn
    pkgs.python310Packages.pillow
    pkgs.python310Packages.rembg
    pkgs.python310Packages.multidict
  ];
}
