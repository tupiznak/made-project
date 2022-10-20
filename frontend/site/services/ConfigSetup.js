export class ConfigSetup {
    setup() {
        const config = useRuntimeConfig();
        if (config.serverUrl.indexOf("vercel") !== -1) {
            const currURL = document.URL;
            const pathArray = currURL.split("/");
            const gitPath = pathArray[2].slice(8);
            config.serverUrl = `${pathArray[0]}//made22t4-back${gitPath}`;
        }
        return config
    }
}