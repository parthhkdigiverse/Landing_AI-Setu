import Header from "@/components/Header";
import Footer from "@/components/Footer";

interface PolicyPageProps {
  title: string;
  children: React.ReactNode;
}

const PolicyLayout = ({ title, children }: PolicyPageProps) => (
  <>
    <Header />
    <main>
      <div className="bg-hero text-primary-foreground py-16 text-center">
        <div className="container">
          <h1 className="text-4xl font-extrabold">{title}</h1>
        </div>
      </div>
      <div className="container py-12 max-w-3xl prose prose-slate">
        {children}
      </div>
    </main>
    <Footer />
  </>
);

export const PrivacyPolicy = () => (
  <PolicyLayout title="Privacy Policy">
    <p className="text-muted-foreground">AI-Setu ERP by Harikrushn DigiVerse LLP is committed to protecting your privacy. This policy explains how we collect, use, and safeguard your personal data.</p>
    <h3 className="font-heading font-bold text-foreground mt-6">Information We Collect</h3>
    <p className="text-muted-foreground">We collect name, phone number, email, store details, and usage data to provide and improve our services.</p>
    <h3 className="font-heading font-bold text-foreground mt-6">How We Use Your Data</h3>
    <p className="text-muted-foreground">Your data is used to provide ERP services, customer support, and to send relevant updates about our products.</p>
    <h3 className="font-heading font-bold text-foreground mt-6">Data Security</h3>
    <p className="text-muted-foreground">We use industry-standard encryption and secure cloud infrastructure to protect your data.</p>
  </PolicyLayout>
);

export const TermsConditions = () => (
  <PolicyLayout title="Terms & Conditions">
    <p className="text-muted-foreground">By using AI-Setu ERP, you agree to these terms and conditions. Please read them carefully.</p>
    <h3 className="font-heading font-bold text-foreground mt-6">Service Usage</h3>
    <p className="text-muted-foreground">AI-Setu ERP is licensed for use by authorized retail businesses. Unauthorized redistribution is prohibited.</p>
    <h3 className="font-heading font-bold text-foreground mt-6">Payment Terms</h3>
    <p className="text-muted-foreground">All payments are due upon subscription. Prices are subject to applicable GST.</p>
  </PolicyLayout>
);

export const RefundPolicy = () => (
  <PolicyLayout title="Refund & Cancellation">
    <p className="text-muted-foreground">We strive for complete customer satisfaction. Our refund and cancellation policies are designed to be fair and transparent.</p>
    <h3 className="font-heading font-bold text-foreground mt-6">Cancellation</h3>
    <p className="text-muted-foreground">You may cancel your subscription at any time. Access continues until the end of your current billing period.</p>
    <h3 className="font-heading font-bold text-foreground mt-6">Refunds</h3>
    <p className="text-muted-foreground">Refund requests are evaluated on a case-by-case basis within 30 days of purchase.</p>
  </PolicyLayout>
);

export const DataSecurity = () => (
  <PolicyLayout title="Data Security & Backup">
    <p className="text-muted-foreground">Your business data security is our top priority. We implement enterprise-grade security measures.</p>
    <h3 className="font-heading font-bold text-foreground mt-6">Cloud Security</h3>
    <p className="text-muted-foreground">All data is stored on secure cloud servers with 256-bit SSL encryption and regular security audits.</p>
    <h3 className="font-heading font-bold text-foreground mt-6">Automatic Backups</h3>
    <p className="text-muted-foreground">Your data is automatically backed up daily with point-in-time recovery capabilities.</p>
  </PolicyLayout>
);

export const SupportService = () => (
  <PolicyLayout title="Support & Service">
    <p className="text-muted-foreground">We provide comprehensive support to ensure your business runs smoothly with AI-Setu ERP.</p>
    <h3 className="font-heading font-bold text-foreground mt-6">24/7 Support</h3>
    <p className="text-muted-foreground">Our support team is available round the clock via phone, email, and live chat.</p>
    <h3 className="font-heading font-bold text-foreground mt-6">Training</h3>
    <p className="text-muted-foreground">Complete onboarding training is included with your subscription at no additional cost.</p>
  </PolicyLayout>
);
