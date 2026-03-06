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

const Index = () => (
  <>
    <Header />
    <main>
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

export default Index;
