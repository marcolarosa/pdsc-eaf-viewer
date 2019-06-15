"use strict";

export async function loadIndex({ store }) {
    const index = (await get(mapRepositoryRoot("/repository/index.json")))
        .statistics;
    store.commit(`saveIndex`, { index });

    async function get(path) {
        try {
            let response = await fetch(path);
            if (response.status !== 200) {
                throw new Error(response);
            }
            return await response.json();
        } catch (error) {
            console.log(error);
            return [];
        }
    }
}

export async function loadFileData({ dataFile }) {
    let response = await fetch(mapRepositoryRoot(dataFile));
    if (response.status !== 200) {
        throw new Error(response);
    }
    let data = await response.json();
    return data;
}

export function mapRepositoryRoot(path) {
    const root =
        process.env.NODE_ENV === "development"
            ? "/repository"
            : "/elan-lint/repository";
    return path.replace("/repository", root);
}
