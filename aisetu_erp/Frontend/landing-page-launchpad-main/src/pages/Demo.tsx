import Header from "@/components/Header";
import Footer from "@/components/Footer";
import DemoForm from "@/components/DemoForm";

const Demo = () => (
  <>
    <Header />
    <main className="min-h-[80vh] flex items-center justify-center bg-background py-16">
      <div className="w-full max-w-sm bg-card rounded-2xl p-8 shadow-card border border-border">
        <h1 className="font-heading font-bold text-2xl text-foreground mb-1">Book A Free Demo</h1>
        <p className="text-sm text-muted-foreground mb-6">Fill the form and our team will contact you shortly.</p>
        <DemoForm />
      </div>
    </main>
    <Footer />
  </>
);

export default Demo;
