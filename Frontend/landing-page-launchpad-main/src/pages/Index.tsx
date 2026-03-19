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

        {/* Pass preview data ONLY to hero */}
        <HeroSection />
        <TrustStrip />
        <ProblemSection />
        <SolutionSection />
        <USPSection />
        <HowItWorks />
        <WhoIsThisFor />
        <PricingSection />
        <ReferralSection />
        <ComparisonSection />
        <TestimonialsSection />
        <FAQSection />
        <FinalCTA />

      </main>

      <Footer />
    </>
  );
};

export default Index;