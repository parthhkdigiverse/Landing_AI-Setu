import axios from "axios";

// Use hardcoded backend URL for local development
export const API_BASE_URL = 'http://127.0.0.1:8000';

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
    trust_item1: string;
    trust_item2: string;
    trust_item3: string;
    trust_item4: string;
    problem_section_label: string;
    problem_section_title: string;
    solution_section_label: string;
    solution_section_title: string;
    nobarcode_label: string;
    nobarcode_title: string;
    nobarcode_desc: string;
    usp_badge_text: string;
    usp_title: string;
    usp_description: string;
    howitworks_label: string;
    howitworks_title: string;
    howitworks_desc: string;
    who_main_title: string;
    who_title: string;
    pricing_main_title: string;
    pricing_main_desc: string;
    pricing_label: string;
    pricing_title: string;
    pricing_plan_name1: string;
    pricing_old_price1: string;
    pricing_price1: string;
    pricing_price_suffix1: string;
    pricing_feature1_1: string;
    pricing_feature1_2: string;
    pricing_feature1_3: string;
    pricing_feature1_4: string;
    pricing_feature1_5: string;
    pricing_feature1_6: string;
    pricing_feature1_7: string;
    pricing_feature1_8: string;
    referral_main_title: string;
    referral_main_desc: string;
    referral_label: string;
    refrerral_title: string;
    join_referral: string;
    comparision_title: string;
    comparison_subtitle: string;
    comparison_title1: string;
    comparison_title2: string;
    comparison_title3: string;
    testimonial_label: string;
    testimonial_title: string;
    review_button: string;
    all_reviews_title: string;
    all_reviews_desc: string;
    faq_label: string;
    faq_title: string;
    cta_badge: string;
    cta_title: string;
    cta_description: string;
    cta_button_text: string;
    cta_small_text: string;
    feature_title: string;
    feature_title2: string;

}

export const fetchLandingPageContent = async (): Promise<LandingPageContent | null> => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/landing-content/?t=${Date.now()}`);
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

export const fetchProblems = async (): Promise<any[]> => {
    try {
        const res = await fetch(`${API_BASE_URL}/api/problems/?t=${Date.now()}`);
        if (!res.ok) throw new Error("Failed to fetch problems");
        return await res.json();
    } catch (error) {
        console.error(error);
        return [];
    }
};

export const fetchSolutions = async (): Promise<any[]> => {
    try {
        const res = await fetch(`${API_BASE_URL}/api/features/?t=${Date.now()}`);
        if (!res.ok) throw new Error("Failed to fetch solutions");
        return await res.json();
    } catch (error) {
        console.error(error);
        return [];
    }
};

export const fetchUSPFeatures = async (): Promise<any[]> => {
    try {
        const res = await fetch(`${API_BASE_URL}/api/usp-features/?t=${Date.now()}`);
        if (!res.ok) throw new Error("Failed to fetch USP features");
        return await res.json();
    } catch (error) {
        console.error(error);
        return [];
    }
};

export const fetchHowItWorks = async (): Promise<any[]> => {
    try {
        const res = await fetch(`${API_BASE_URL}/api/how-it-works/?t=${Date.now()}`);
        if (!res.ok) throw new Error("Failed to fetch how it works steps");
        return await res.json();
    } catch (error) {
        console.error(error);
        return [];
    }
};

export const fetchStoreTypes = async (): Promise<any[]> => {
    try {
        const res = await fetch(`${API_BASE_URL}/api/store-types/?t=${Date.now()}`);
        if (!res.ok) throw new Error("Failed to fetch store types");
        return await res.json();
    } catch (error) {
        console.error(error);
        return [];
    }
};

export const fetchReferralPerks = async (): Promise<any[]> => {
    try {
        const res = await fetch(`${API_BASE_URL}/api/referral-perks/?t=${Date.now()}`);
        if (!res.ok) throw new Error("Failed to fetch referral perks");
        return await res.json();
    } catch (error) {
        console.error(error);
        return [];
    }
};

export const fetchHomeTestimonials = async (): Promise<any[]> => {
    try {
        const res = await fetch(`${API_BASE_URL}/api/home-testimonials/?t=${Date.now()}`);
        if (!res.ok) throw new Error("Failed to fetch home testimonials");
        return await res.json();
    } catch (error) {
        console.error(error);
        return [];
    }
};

export const fetchAllTestimonials = async (): Promise<any[]> => {
    try {
        const res = await fetch(`${API_BASE_URL}/api/testimonials/?t=${Date.now()}`);
        if (!res.ok) throw new Error("Failed to fetch all testimonials");
        return await res.json();
    } catch (error) {
        console.error(error);
        return [];
    }
};


// export interface AboutPageContent {
//     id: number;
//     hero_title: string;
//     hero_description: string;
//     about_label: string;
//     about_heading: string;
//     about_description_1: string;
//     about_description_2: string;
//     about_description_3: string;
//     mission_title: string;
//     mission_description: string;
//     why_choose_title: string;
//     why_point_1: string;
//     why_point_2: string;
//     why_point_3: string;
//     why_point_4: string;
//     why_point_5: string;
//     serve_title: string;
//     serve_subtitle: string;
//     serve1_title: string;
//     serve2_title: string;
//     serve3_title: string;
//     serve4_title: string;
//     cta_title: string;
//     cta_description: string;
//     cta_button_text: string;
    
// }

// export const fetchAboutPageContent = async (): Promise<AboutPageContent | null> => {
//   try {
//     const res = await fetch(`${API_BASE_URL}/api/about-page/?t=${Date.now()}`);
//     if (!res.ok) throw new Error("Failed");

//     return await res.json();
//   } catch (error) {
//     console.error(error);
//     return null;
//   }
// };

export interface ContactPageContent {
  hero_title: string;
  hero_description: string;
  call_title: string;
  call_phone: string;
  call_phone_number: string;
  call_subtext: string;
  email_title: string;
  email_address: string;
  email_address_link: string;
  email_subtext: string;
  visit_title: string;
  visit_address: string;
  visit_subtext: string;
  visit_map_url: string;
  support_title: string;
  support_time: string;
  support_subtext: string;
  form_title: string;
  name_label: string;
  name_placeholder: string;
  phone_label: string;
  phone_placeholder: string;
  email_label: string;
  email_placeholder: string;
  company_label: string;
  company_placeholder: string;
  message_label: string;
  message_placeholder: string;
  form_button_text: string;
  why_title: string;
  why_description: string;
  feature_1_title: string;
  feature_2_title: string;
  feature_3_title: string;
  feature_4_title: string;
  cta_title: string;
  cta_description: string;
  cta_button_text1: string;
  cta_button_text2: string;
  cta_button_text3: string;
}

export const fetchContactPageContent = async (): Promise<ContactPageContent | null> => {
  try {
    // Adding a timestamp here also helps prevent stale data
    const res = await fetch(`${API_BASE_URL}/api/contactus-page/?t=${Date.now()}`);
    if (!res.ok) throw new Error("Failed");
    return await res.json();
  } catch (error) {
    console.error(error);
    return null;
  }
};

export interface BlogCategory {
    id: number;
    name: string;
    slug: string;
}

export interface BlogPost {
    id: number;
    title: string;
    slug: string;
    category_name: string;
    featured_image_url: string;
    excerpt: string;
    content: string;
    author: string;
    created_at: string;
    is_published: boolean;
}

export const fetchBlogPosts = async (categorySlug?: string): Promise<BlogPost[]> => {
    try {
        const url = categorySlug 
            ? `${API_BASE_URL}/api/blogs/?category=${categorySlug}&t=${Date.now()}`
            : `${API_BASE_URL}/api/blogs/?t=${Date.now()}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error("Failed to fetch blog posts");
        return await response.json();
    } catch (error) {
        console.error("Failed to fetch blog posts:", error);
        return [];
    }
};

export const fetchBlogPostDetail = async (slug: string): Promise<BlogPost | null> => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/blogs/${slug}/?t=${Date.now()}`);
        if (!response.ok) throw new Error("Failed to fetch blog post detail");
        return await response.json();
    } catch (error) {
        console.error("Failed to fetch blog post detail:", error);
        return null;
    }
};

export const fetchBlogCategories = async (): Promise<BlogCategory[]> => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/blog-categories/?t=${Date.now()}`);
        if (!response.ok) throw new Error("Failed to fetch blog categories");
        return await response.json();
    } catch (error) {
        console.error("Failed to fetch blog categories:", error);
        return [];
    }
};



export interface DemoVideo {
  id: string
  title: string
  video_url: string
}

export const fetchDemoVideo = async (): Promise<DemoVideo | null> => {

  try {

    const res = await fetch("http://127.0.0.1:8000/api/demo-video/")

    const data = await res.json()

    return data

  } catch (error) {

    console.error("Failed to load demo video", error)

    return null
  }
}

const API_BASE = "http://127.0.0.1:8000/api";

// ---------------- TYPES ----------------

export interface Culture {
  title: string;
  description: string;
}

export interface Perk {
  title: string;
}

export interface Job {
  title: string;
  experience: string;
  total_positions: number;
  work_place: string;
  location: string;
  slug: string;
  job_slug: string;
}

export interface CareerPageContent {
  hero_title: string;
  hero_subtitle: string;

  culture_title: string;
  cultures: Culture[];

  perks_title: string;
  perks: Perk[];

  positions_title: string;
  jobs: Job[];

  cta_title: string;
  cta_subtitle: string;
  cta_button_text: string;
}

// ---------------- API CALL ----------------

export const fetchCareerPageContent = async (): Promise<CareerPageContent | null> => {
  try {
    const response = await axios.get(`${API_BASE}/career/`);
    return response.data;
  } catch (error) {
    console.error("Failed to load career page content:", error);
    return null;
  }
};

export const fetchJobDetails = async (slug: string) => {

  const res = await fetch(
    `http://127.0.0.1:8000/api/job/${slug}/`
  );

  return res.json();
};

// const API_BASE = "http://127.0.0.1:8000/api";

// ================= TYPES =================

export interface SectionItem {
  id: number;
  title?: string;
  description?: string;
  image?: string;
  order: number;
}

export interface Section {
  id: number;
  name: string;
  title?: string;
  subtitle?: string;
  image?: string;
  order: number;
  items: SectionItem[];
}

export interface AboutPageContent {
  id: number;
  title: string;
  slug: string;
  sections: Section[];
}

// ================= API =================

export const fetchAboutPageContent = async (): Promise<AboutPageContent | null> => {
  try {
    const res = await fetch(`${API_BASE}/pages/about/?t=${Date.now()}`);

    if (!res.ok) throw new Error("Failed to fetch");

    const data = await res.json();

    // ✅ FIX IMAGE URLS
    data.sections = data.sections.map((section: Section) => ({
      ...section,
      image: section.image
        ? `http://127.0.0.1:8000${section.image}`
        : null,
      items: section.items.map((item: SectionItem) => ({
        ...item,
        image: item.image
          ? `http://127.0.0.1:8000${item.image}`
          : null,
      })),
    }));

    return data;
  } catch (error) {
    console.error("API ERROR:", error);
    return null;
  }
};

const BASE_URL = "http://127.0.0.1:8000/api";

// ==============================
// TYPES
// ==============================

export interface PolicySection {
  id: number;
  heading: string;
  content: string;
  order: number;
}

export interface Policy {
  id: number;
  title: string;
  slug: string;
  description: string;
  sections: PolicySection[];
}

// ==============================
// COMMON FETCH FUNCTION
// ==============================

const fetchAPI = async (endpoint: string) => {
  try {
    const res = await fetch(`${BASE_URL}${endpoint}`);

    if (!res.ok) {
      throw new Error(`Error: ${res.status}`);
    }

    return await res.json();
  } catch (error) {
    console.error("API ERROR:", error);
    return null;
  }
};

// ==============================
// POLICY APIs
// ==============================

// ✅ Get ALL policies
export const fetchPolicies = async (): Promise<Policy[] | null> => {
  return fetchAPI("/policies/");
};

// ✅ Get SINGLE policy by slug
export const fetchPolicy = async (slug: string): Promise<Policy | null> => {
  return fetchAPI(`/policies/${slug}/`);
};