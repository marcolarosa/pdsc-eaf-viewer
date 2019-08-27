> # Development of this application has moved to https://github.com/CoEDL/eaf-viewer
>
> ## Issues raised here will be ignored.

- [EAF Viewer](#eaf-viewer)
  - [Developing the application](#developing-the-application)
  - [Vue application](#vue-application)
  - [Building a release for MacOS](#building-a-release-for-macos)
  - [Publishing release to github releases](#publishing-release-to-github-releases)
  - [Electron webpack](#electron-webpack)

# EAF Viewer

An application to process a folder of EAF files and visualise file statistics to reveal incomplete files and missing data.

This is an electron application.

## Developing the application

```
> npm run install
> npm run develop
```

## Vue application

The application itself is built using VueJS, Vue Router and Vuex. See the respective sites for more
information.

## Building a release for MacOS

```
> npm run build:mac
```

## Publishing release to github releases

For this you will need a Github Personal Access Token. See github for more information. You will be
asked if you want to bump the minor version (say yes if you haven't already done it) before building
the relevant versions (as outlined above) and publishing them to github releases.

```
> ./bin/publish-release.sh
```

After the release has been built navigate to [https://github.com/marcolarosa/pdsc-eaf-viewer/releases](https://github.com/marcolarosa/pdsc-eaf-viewer/releases)
and check the artifacts are ok, then `Edit` and `Publish release`.

## Electron webpack

This application is built using [electron builder](https://www.electron.build/) and
[electron-webpack](https://webpack.electron.build/). See the respective links if you need to
alter the configuration.
