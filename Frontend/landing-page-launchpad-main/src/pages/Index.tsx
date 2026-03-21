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

    const handler = (event: MessageEvent) => {
      if (event.data && typeof event.data === 'object' && !Array.isArray(event.data) && event.data.source === 'django-admin') {
        setContent((prev: any) => ({
          ...prev,
          ...event.data.payload
        }));
        if (event.data.scrollTarget) {
          setTimeout(() => {
            const el = document.getElementById(event.data.scrollTarget);
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }, 100);
        }
      }
    };

    window.addEventListener("message", handler);

    return () => window.removeEventListener("message", handler);

  }, []);

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
        <div id="hero"><HeroSection /></div>
        <div id="trusted-retailers"><TrustStrip /></div>
        <div id="problem"><ProblemSection /></div>
        <div id="solution"><SolutionSection /></div>
        <div id="usp"><USPSection /></div>
        <div id="how-it-works"><HowItWorks /></div>
        <div id="who-is-this-for"><WhoIsThisFor /></div>
        <div id="pricing"><PricingSection /></div>
        <div id="referral"><ReferralSection /></div>
        <div id="comparison"><ComparisonSection /></div>
        <div id="testimonials"><TestimonialsSection /></div>
        <div id="faq"><FAQSection /></div>
        <div id="cta"><FinalCTA /></div>
      </main>

      <Footer />
    </>
  );
};

export default Index;