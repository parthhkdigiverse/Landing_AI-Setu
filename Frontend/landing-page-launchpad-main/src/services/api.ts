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
    faq_title: string;
    faq1_question: string;
    faq1_answer: string;
    faq2_question: string;
    faq2_answer: string;
    faq3_question: string;
    faq3_answer: string;
    faq4_question: string;
    faq4_answer: string;
    faq5_question: string;
    faq5_answer: string;
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


export interface AboutPageContent {
    id: number;
    hero_title: string;
    hero_description: string;
    about_label: string;
    about_heading: string;
    about_description_1: string;
    about_description_2: string;
    about_description_3: string;
    mission_title: string;
    mission_description: string;
    why_choose_title: string;
    why_point_1: string;
    why_point_2: string;
    why_point_3: string;
    why_point_4: string;
    why_point_5: string;
    serve_title: string;
    serve_subtitle: string;
    serve1_title: string;
    serve2_title: string;
    serve3_title: string;
    serve4_title: string;
    cta_title: string;
    cta_description: string;
    cta_button_text: string;
    
}

export const fetchAboutPageContent = async (): Promise<AboutPageContent | null> => {
  try {
    const res = await fetch("http://127.0.0.1:8000/api/about-page/");
    if (!res.ok) throw new Error("Failed");

    return await res.json();
  } catch (error) {
    console.error(error);
    return null;
  }
};

export interface CareerPageContent {
    id: string;
    hero_title: string;
    hero_description: string;
    culture_title: string;
    culture_1_title: string;
    culture_1_desc: string;
    culture_2_title: string;
    culture_2_desc: string;
    culture_3_title: string;
    culture_3_desc: string;
    culture_4_title: string;
    culture_4_desc: string;
    benefits_title: string;
    benefit_1: string;
    benefit_2: string;
    benefit_3: string;
    benefit_4: string;
    benefit_5: string;
    benefit_6: string;
    positions_title: string;
    job_1_role: string;
    job_1_details: string;
    job_2_role: string;
    job_2_details: string;
    job_3_role: string;
    job_3_details: string;
    cta_title: string;
    cta_description: string;
    cta_button_text: string;

}

export const fetchCareerPageContent = async (): Promise<CareerPageContent | null> => {
  try {
    // Adding a timestamp here also helps prevent stale data
    const res = await fetch(`http://127.0.0.1:8000/api/career-page/?t=${Date.now()}`);
    if (!res.ok) throw new Error("Failed");
    return await res.json();
  } catch (error) {
    console.error(error);
    return null;
  }
};


export interface ContactPageContent {
  hero_title: string;
  hero_description: string;
  call_title: string;
  call_phone: string;
  call_subtext: string;
  email_title: string;
  email_address: string;
  email_subtext: string;
  visit_title: string;
  visit_address: string;
  visit_subtext: string;
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
    const res = await fetch(`http://127.0.0.1:8000/api/contactus-page/?t=${Date.now()}`);
    if (!res.ok) throw new Error("Failed");
    return await res.json();
  } catch (error) {
    console.error(error);
    return null;
  }
};