import Header from "@/components/Header";
import Footer from "@/components/Footer";
import SolutionSection from "@/components/landing/SolutionSection";
import USPSection from "@/components/landing/USPSection";
import ComparisonSection from "@/components/landing/ComparisonSection";

const Features = () => (
  <>
    <Header />
    <main>
      <div className="bg-hero text-primary-foreground py-16 text-center">
        <div className="container">
          <h1 className="text-4xl lg:text-5xl font-extrabold mb-4">Features</h1>
          <p className="text-primary-foreground/70 max-w-lg mx-auto">Everything you need to run your retail business smarter.</p>
        </div>
      </div>
      <SolutionSection />
      <USPSection />
      <ComparisonSection />
    </main>
    <Footer />
  </>
);

export default Features;
