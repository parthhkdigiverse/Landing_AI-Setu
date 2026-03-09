import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import Features from "./pages/Features";
import Pricing from "./pages/Pricing";
import Referral from "./pages/Referral";
import Login from "./pages/Login";
import Demo from "./pages/Demo";
import PricingSignup from "./pages/PricingSignup";
import { PrivacyPolicy, TermsConditions, RefundPolicy, DataSecurity, SupportService } from "./pages/PolicyPages";
import { About, Blog, Career, Contact } from "./pages/ComingSoon";
import NotFound from "./pages/NotFound";
import JobDetails from "@/pages/JobDetails";
import ApplyJob from "./pages/ApplyJob";
import ReferralPage from "@/components/landing/ReferralSection";
import BlogPost from "./pages/BlogPost"; // import new blog post detail component

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/features" element={<Features />} />
          <Route path="/pricing" element={<Pricing />} />
          <Route path="/referral" element={<Referral />} />
          <Route path="/login" element={<Login />} />
          <Route path="/demo" element={<Demo />} />
          <Route path="/privacy" element={<PrivacyPolicy />} />
          <Route path="/terms" element={<TermsConditions />} />
          <Route path="/refund" element={<RefundPolicy />} />
          <Route path="/data-security" element={<DataSecurity />} />
          <Route path="/support" element={<SupportService />} />
          <Route path="/about" element={<About />} />
          <Route path="/blog" element={<Blog />} />
          <Route path="/blog/:postId" element={<BlogPost />} />
          <Route path="/career" element={<Career />} />
          <Route path="/career/:jobId" element={<JobDetails />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="*" element={<NotFound />} />
          <Route path="/pricing-signup" element={<PricingSignup />} />
          <Route path="/career/apply/:jobId" element={<ApplyJob />} />
          <Route path="/referral" element={<ReferralPage />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
