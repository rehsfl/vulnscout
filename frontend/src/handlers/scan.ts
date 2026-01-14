/**
 * Handler for triggering a new scan
 */

/**
 * Trigger a new scan by calling the backend API
 * @returns Promise with the response data
 */
async function triggerScan(): Promise<{ status: string; message: string }> {
    const response = await fetch(import.meta.env.VITE_API_URL + "/api/scan/trigger", {
        method: 'POST',
        mode: "cors",
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to trigger scan');
    }

    return await response.json();
}

export { triggerScan };
