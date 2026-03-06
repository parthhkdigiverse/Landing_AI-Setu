import Header from "@/components/Header";
import Footer from "@/components/Footer";
import ReferralSection from "@/components/landing/ReferralSection";
import FAQSection from "@/components/landing/FAQSection";

const Referral = () => (
  <>
    <Header />
    <main>
      <div className="bg-hero text-primary-foreground py-16 text-center">
        <div className="container">
          <h1 className="text-4xl lg:text-5xl font-extrabold mb-4">Referral Program</h1>
          <p className="text-primary-foreground/70 max-w-lg mx-auto">Earn money by referring retailers to AI-Setu ERP.</p>
        </div>
      </div>
      <ReferralSection />
      <FAQSection />
    </main>
    <Footer />
  </>
);

export default Referral;
