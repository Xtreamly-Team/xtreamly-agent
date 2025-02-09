const API_URL = 'https://xtreamly-agent-664616721985.us-central1.run.app/path';
// const API_URL = 'http://localhost:8000/path';

function getUrl(path: string, params: any = {}) {
    const url = new URL(`${API_URL.replace("path", path)}`)
    url.search = new URLSearchParams(params).toString();
    return url
}

export function get(path: string, params: any = {}) {
    return fetch(getUrl(path, params))
}

export function post(path: string, params: any = {}, body: any = {}) {
    return fetch(getUrl(path, params), {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    })
}
