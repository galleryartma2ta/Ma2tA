export const load = async ({ fetch }) => {
    try {
        const response = await fetch('http://localhost:8080/api/v1/categories');
        const categories = await response.json();
        
        return {
            categories
        };
    } catch (error) {
        return {
            categories: []
        };
    }
}