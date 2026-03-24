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

import { fetchLandingPageContent, LandingPageContent } from "@/services/api";

const Index = () => {

  const [content, setContent] = useState<LandingPageContent | null>(null);

  useEffect(() => {
    const loadContent = async () => {
      const data = await fetchLandingPageContent();
      if (data) {
        setContent(data);
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
          setContent((prev: any) => ({
            ...prev,
            ...payload
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
  const shouldShow = (id: string) => {
    if (!isPreview || !sectionParam) return true;
    return sectionParam === id;
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
      <DemoPopup />
      <Header />

      <main>
        {shouldShow('hero') && <div id="hero"><HeroSection /></div>}
        {shouldShow('trusted-retailers') && <div id="trusted-retailers"><TrustStrip /></div>}
        {shouldShow('problem') && <div id="problem"><ProblemSection /></div>}
        {shouldShow('solution') && <div id="solution"><SolutionSection /></div>}
        {shouldShow('usp') && <div id="usp"><USPSection /></div>}
        {shouldShow('how-it-works') && <div id="how-it-works"><HowItWorks /></div>}
        {shouldShow('who-is-this-for') && <div id="who-is-this-for"><WhoIsThisFor /></div>}
        {shouldShow('pricing') && <div id="pricing"><PricingSection /></div>}
        {shouldShow('referral') && <div id="referral"><ReferralSection /></div>}
        {shouldShow('comparison') && <div id="comparison"><ComparisonSection /></div>}
        {shouldShow('testimonials') && <div id="testimonials"><TestimonialsSection /></div>}
        {shouldShow('faq') && <div id="faq"><FAQSection /></div>}
        {shouldShow('cta') && <div id="cta"><FinalCTA /></div>}
      </main>

      {(!isPreview || !sectionParam) && <Footer />}
    </>
  );
};

export default Index;