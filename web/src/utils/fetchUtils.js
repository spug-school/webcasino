/* fetch utility functions */
import { apiUrl } from "../core/config.js";

const fetchData = async (url, options = {}) => {
    try {
        const response = await fetch(url, {
            method: options.method || "GET",
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            ...options,
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
    }
}

// player data
export const getPlayerData = async () => {
    const url = `${apiUrl}/player`;
    return fetchData(url);
}

// leaderboard
export const getLeaderBoardData = async (queryParams) => {
    const params = new URLSearchParams(queryParams).toString();
    const url = `${apiUrl}/leaderboard?${params}`;
    return fetchData(url);
}

// gamehistory
export const getGameHistory = async () => {
    const url = `${apiUrl}/gamehistory`;
    return fetchData(url);
}