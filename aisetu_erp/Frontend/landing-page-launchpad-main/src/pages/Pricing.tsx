import Header from "@/components/Header";
import Footer from "@/components/Footer";
import PricingSection from "@/components/landing/PricingSection";
import FAQSection from "@/components/landing/FAQSection";

const Pricing = () => (
  <>
    <Header />
    <main>
      <div className="bg-hero text-primary-foreground py-16 text-center">
        <div className="container">
          <h1 className="text-4xl lg:text-5xl font-extrabold mb-4">Pricing</h1>
          <p className="text-primary-foreground/70 max-w-lg mx-auto">Simple, transparent pricing — one package, everything included.</p>
        </div>
      </div>
      <PricingSection />
      <FAQSection />
    </main>
    <Footer />
  </>
);

export default Pricing;
