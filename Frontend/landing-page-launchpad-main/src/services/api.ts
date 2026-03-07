// Use relative URL so it works regardless of host (dev or production)
export const API_BASE_URL = '';

export interface LandingPageContent {
    id: number;
    hero_eyebrow: string;
    hero_title: string;
    hero_highlighted_title: string;
    hero_subtitle: string;
    hero_highlights: string; // comma separated
    primary_cta_text: string;
    secondary_cta_text: string;
    trusted_retailers_count: string;
    hero_stats_label: string;
    hero_stats_value: string;
}

export const fetchLandingPageContent = async (): Promise<LandingPageContent | null> => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/landing-content/`);
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Failed to fetch landing page content:", error);
        return null;
    }
};
