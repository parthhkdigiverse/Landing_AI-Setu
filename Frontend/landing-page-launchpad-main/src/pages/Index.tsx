import { useEffect, useState } from "react";

import Header from "@/components/Header";
import Footer from "@/components/Footer";
import HeroSection from "@/components/landing/HeroSection";
import TrustStrip from "@/components/landing/TrustStrip";
import ProblemSection from "@/components/landing/ProblemSection";
import SolutionSection from "@/components/landing/SolutionSection";
import USPSection from "@/components/landing/USPSection";
import HowItWorks from "@/components/landing/HowItWorks";
import WhoIsThisFor from "@/components/landing/WhoIsThisFor";
import PricingSection from "@/components/landing/PricingSection";
import ReferralSection from "@/components/landing/ReferralSection";
import ComparisonSection from "@/components/landing/ComparisonSection";
import TestimonialsSection from "@/components/landing/TestimonialsSection";
import FAQSection from "@/components/landing/FAQSection";
import FinalCTA from "@/components/landing/FinalCTA";
import DemoPopup from "@/components/DemoPopup";
import SEO from "@/components/SEO";
import { LandingSkeleton } from "@/components/landing/LandingSkeleton";

import { fetchLandingPageContent, LandingPageContent } from "@/services/api";

const Index = () => {

  const [content, setContent] = useState<LandingPageContent | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadContent = async () => {
      try {
        const data = await fetchLandingPageContent();
        if (data) {
          setContent(data);
        }
      } finally {
        setIsLoading(false);
      }
    };
    loadContent();
  }, []);

  useEffect(() => {
    const previewChannel = new BroadcastChannel('aisetu_preview');

    const handler = (event: MessageEvent) => {
      if (event.data && typeof event.data === 'object' && !Array.isArray(event.data) && event.data.source === 'django-admin') {
        
        if (event.data.model === 'LandingPageContent' || 
            event.data.model === 'PricingContent' || 
            event.data.model === 'ChallengeContent' || 
            event.data.model === 'SolutionContent' ||
            event.data.model === 'USPContent' || 
            event.data.model === 'HowItWorksContent' || 
            event.data.model === 'WhoIsThisForContent' || 
            event.data.model === 'TestimonialContent' || 
            event.data.model === 'ComparisonContent' || 
            event.data.model === 'FAQContent' || 
            event.data.model === 'TrustContent' || 
            event.data.model === 'HeroContent' || 
            event.data.model === 'CTAContent' || 
            event.data.model === 'ReferralProgramContent') {
          
          const payload = event.data.payload;
          const cleanedPayload = { ...payload };
          
          // Global Filter: Remove items marked for deletion in any array (formsets)
          Object.keys(cleanedPayload).forEach(key => {
            if (Array.isArray(cleanedPayload[key])) {
                cleanedPayload[key] = cleanedPayload[key].filter((item: any) => !item.DELETE);
            }
          });

          setContent((prev: any) => ({
            ...prev,
            ...cleanedPayload
          }));

          // Broadcast to other tabs
          previewChannel.postMessage({
            type: 'LIVE_PREVIEW_UPDATE',
            content: payload
          });
        }

        if (event.data.scrollTarget) {
          setTimeout(() => {
            const el = document.getElementById(event.data.scrollTarget);
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }, 100);
        }
      }
    };

    const channelHandler = (event: MessageEvent) => {
      if (event.data?.type === 'LIVE_PREVIEW_UPDATE') {
        setContent((prev: any) => ({
          ...prev,
          ...event.data.content
        }));
      }
    };

    window.addEventListener("message", handler);
    previewChannel.addEventListener("message", channelHandler);

    return () => {
      window.removeEventListener("message", handler);
      previewChannel.removeEventListener("message", channelHandler);
      previewChannel.close();
    };

  }, []);

  const isPreview = typeof window !== 'undefined' ? new URLSearchParams(window.location.search).get('is_preview') === '1' : false;
  const sectionParam = typeof window !== 'undefined' ? new URLSearchParams(window.location.search).get('section') : null;

  // Helper to determine if a section should be shown
  const shouldShow = (id: string, toggle?: boolean) => {
    // If it's a preview for a specific section, always show it
    if (isPreview && sectionParam === id) return true;
    
    // If we have a toggle from the backend, respect it
    if (toggle === false) return false;

    // Standard preview logic
    if (isPreview && sectionParam && sectionParam !== id) return false;

    return true;
  };

  // Mount scroll to section param
  useEffect(() => {
    if (sectionParam) {
      setTimeout(() => {
        const el = document.getElementById(sectionParam);
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 800); // Wait for components to load
    }
  }, [sectionParam]);

  return (
    <>
      <SEO 
        title={content?.seo_title || "Home"} 
        description={content?.seo_description || "AI Setu - Empowering your business with AI-driven solutions and seamless automation. Scale your operations effortlessly."}
        keywords={content?.seo_keywords || "AI, automation, business solutions, AI Setu"}
      />
      {(!isPreview || !sectionParam) && <DemoPopup />}
      {(!isPreview || !sectionParam) && <Header />}

      {isLoading ? (
        <LandingSkeleton />
      ) : (
        <main>
          {shouldShow('hero', content?.show_hero) && <div id="hero"><HeroSection content={content} /></div>}
          {shouldShow('trusted-retailers', content?.show_trust_strip) && <div id="trusted-retailers"><TrustStrip content={content} /></div>}
          {shouldShow('problem', content?.show_problem) && <div id="problem"><ProblemSection content={content} /></div>}
          {shouldShow('solution', content?.show_solution) && <div id="solution"><SolutionSection content={content} /></div>}
          {shouldShow('usp', content?.show_usp) && <div id="usp"><USPSection content={content} /></div>}
          {shouldShow('how-it-works', content?.show_how_it_works) && <div id="how-it-works"><HowItWorks content={content} /></div>}
          {shouldShow('who-is-this-for', content?.show_who_is_this_for) && <div id="who-is-this-for"><WhoIsThisFor content={content} /></div>}
          {shouldShow('pricing', content?.show_pricing) && <div id="pricing"><PricingSection content={content} /></div>}
          {shouldShow('referral', content?.show_referral) && <div id="referral"><ReferralSection content={content} /></div>}
          {shouldShow('comparison', content?.show_comparison) && <div id="comparison"><ComparisonSection content={content} /></div>}
          {shouldShow('testimonials', content?.show_testimonials) && <div id="testimonials"><TestimonialsSection content={content} /></div>}
          {shouldShow('faq', content?.show_faq) && <div id="faq"><FAQSection content={content} /></div>}
          {shouldShow('cta', content?.show_cta) && <div id="cta"><FinalCTA content={content} /></div>}
        </main>
      )}

      {(!isPreview || !sectionParam || sectionParam === 'footer' || sectionParam === 'master-footer') && <Footer />}
    </>
  );
};

export default Index;