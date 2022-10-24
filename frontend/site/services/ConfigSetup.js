import {useRuntimeConfig} from "nuxt/app";

export class ConfigSetup {
    setup() {
        // when returning value to another file via mounted, serverUrl property is not found by the key
        const config = useRuntimeConfig();
        if (config.serverUrl.indexOf("vercel") !== -1) {
            const currURL = document.URL;
            const pathArray = currURL.split("/");
            const gitPath = pathArray[2].slice(8);
            config.serverUrl = `${pathArray[0]}//made22t4-back${gitPath}`;
        }
        return config
    }

    getServerUrl() {
        const config = this.setup()
        return config.serverUrl
    }
}