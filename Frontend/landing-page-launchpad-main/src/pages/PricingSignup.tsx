import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { ArrowLeft } from "lucide-react";
import { API_BASE_URL, fetchLandingPageContent } from "@/services/api";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import SolutionSection from "@/components/landing/SolutionSection";
import USPSection from "@/components/landing/USPSection";
import ComparisonSection from "@/components/landing/ComparisonSection";
import { useToast } from "@/components/ui/use-toast";
import SEO from "@/components/SEO";

const PricingSignup = () => {

  const navigate = useNavigate();
  const { toast } = useToast();

  const [formData, setFormData] = useState({
    shopName: "",
    ownerName: "",
    mobileNumber: "",
    referralCode: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;

    setFormData({
      ...formData,
      [name]: value,
    });

    // If referral code field becomes empty → reset price
    if (name === "referralCode" && value === "") {
      setPrice(basePrice * 1.18);
    }
  };

  const handleApplyReferral = async () => {
    if (!formData.referralCode) {
      toast({
        title: "Enter referral code",
        variant: "destructive",
      });
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/pricing-signup/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          referral_code: formData.referralCode,
          check_referral: true
        }),
      });

      const data = await response.json();

      if (data.valid) {
        setPrice(12980);

        toast({
          title: "Referral applied successfully",
        });

      } else {
        toast({
          title: "Invalid referral code",
          variant: "destructive",
        });
      }

    } catch (error) {
      toast({
        title: "Unable to verify referral",
        variant: "destructive",
      });
    }
  };

  const getCSRFToken = () => {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      const [name, value] = cookie.trim().split("=");
      if (name === "csrftoken") return value;
    }
    return "";
  };

  const [loading, setLoading] = useState(false);
  const [basePrice, setBasePrice] = useState(12000);
  const [price, setPrice] = useState(14160);
  const [content, setContent] = useState<any>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        // 1. Fetch Landing Page Content (Pricing)
        const data = await fetchLandingPageContent();
        if (data) {
          setContent(data);
          if (data.pricing_price) {
            const parsedPrice = parseInt(data.pricing_price.replace(/[^0-9]/g, ''), 10);
            if (!isNaN(parsedPrice) && parsedPrice > 0) {
              setBasePrice(parsedPrice);
              setPrice(parsedPrice * 1.18);
            }
          }
        }
      } catch (err) {
        console.error("Failed to load pricing content:", err);
      }
    };
    loadData();

    const previewChannel = new BroadcastChannel('aisetu_preview');

    // Live Preview Listener (postMessage fallback)
    const handleMessage = (event: MessageEvent) => {
      if (event.data?.type === 'LIVE_PREVIEW_UPDATE') {
        updateFromPreview(event.data.content);
      }
    };

    // BroadcastChannel Listener (Cross-tab sync)
    const handleBroadcast = (event: MessageEvent) => {
      if (event.data?.type === 'LIVE_PREVIEW_UPDATE') {
        updateFromPreview(event.data.content);
      }
    };

    const updateFromPreview = (updatedContent: any) => {
        setContent((prev: any) => ({
            ...prev,
            ...updatedContent
        }));
        
        // Update price if it changed in preview
        if (updatedContent.pricing_price) {
          const parsedPrice = parseInt(updatedContent.pricing_price.replace(/[^0-9]/g, ''), 10);
          if (!isNaN(parsedPrice) && parsedPrice > 0) {
            setBasePrice(parsedPrice);
            setPrice(parsedPrice * 1.18);
          }
        }
    };

    window.addEventListener('message', handleMessage);
    previewChannel.addEventListener('message', handleBroadcast);

    return () => {
        window.removeEventListener('message', handleMessage);
        previewChannel.removeEventListener('message', handleBroadcast);
        previewChannel.close();
    };
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      // 1️⃣ Submit signup form
      const response = await fetch(`${API_BASE_URL}/pricing-signup/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          shop_name: formData.shopName,
          owner_name: formData.ownerName,
          mobile_number: formData.mobileNumber,
          referral_code: formData.referralCode,
        }),
      });

      const signupData = await response.json();

      if (!response.ok || signupData.error) {
        alert(signupData.error || "Signup failed");
        setLoading(false);
        return;
      }

      const signupId = signupData.signup_id;

      // 2️⃣ Initiate payment via PhonePe
      const paymentResponse = await fetch(
        `${API_BASE_URL}/phonepe/initiate/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          credentials: "include",
          body: JSON.stringify({
            amount: price,
            phone: formData.mobileNumber,
            signup_id: signupId,
          }),
        }
      );

      const paymentData = await paymentResponse.json();
      console.log("Payment Response:", paymentData);

      if (!paymentResponse.ok) {
        alert(paymentData.error || "Payment initiation failed");
        setLoading(false);
        return;
      }

      if (paymentData.payment_url) {
        window.location.href = paymentData.payment_url;
      } else {
        alert("Payment URL not received from server");
      }
    } catch (error: any) {
      console.error("Error:", error);
      alert("Something went wrong while processing payment");
    }

    setLoading(false);
  };

  return (
    <>
      <SEO 
        title="Complete Your Purchase" 
        description="Finalize your subscription to AI Setu and start transforming your business with AI. Secure checkout powered by PhonePe."
        keywords="checkout, pricing signup, AI Setu subscription, secure payment"
      />
      <Header />

      <div className="min-h-screen pt-24 pb-16 bg-background">
        <div className="container max-w-6xl mx-auto px-4">

          {/* Back Button */}

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">

            {/* Order Summary Side */}
            <div className="bg-card shadow-lg rounded-2xl p-8 border border-border">
              <h2 className="text-2xl font-bold mb-6 text-foreground">Order Summary</h2>
              <div className="text-center mb-8 bg-muted/30 p-6 rounded-xl border border-border/50">
                <p className="text-muted-foreground font-medium mb-1">{content?.pricing_plan_name || "All-Inclusive Package"}</p>

                <div className="flex flex-col items-center justify-center gap-1 mb-2">
                  <div className="bg-green-100 text-green-700 text-xs font-bold px-2 py-0.5 rounded-full mb-1">
                    Save 60%
                  </div>
                  <span className="text-muted-foreground line-through text-lg font-medium tracking-wide">
                    {content?.pricing_old_price || "₹29,999"}
                  </span>
                  <div className="flex items-baseline gap-1 mt-1">
                    <span className="text-5xl font-extrabold text-foreground">
                      ₹{Math.round(price / 1.18).toLocaleString()}
                    </span>
                    <span className="text-muted-foreground text-sm">{content?.pricing_price_suffix || "+ GST"}</span>
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t border-border inline-block min-w-[200px]">
                  <div className="flex justify-between text-sm mb-2 text-muted-foreground line-through opacity-70">
                    <span>MSRP</span>
                    <span>{content?.pricing_old_price || "₹29,999"}</span>
                  </div>
                  <div className="flex justify-between text-sm mb-2 text-foreground font-medium">
                    <span>Offer Price</span>
                    <span>₹{Math.round(price / 1.18).toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between text-sm mb-2 text-muted-foreground">
                    <span>GST (18%)</span>
                    <span>₹{(price - Math.round(price / 1.18)).toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between font-bold text-lg text-foreground mt-3 pt-3 border-t border-dashed border-border/70">
                    <span>Total Amount</span>
                    <span>₹{price.toLocaleString()}</span>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <h3 className="font-semibold text-foreground border-b border-border pb-2">What's Included:</h3>
                <ul className="space-y-3">
                  {(content?.pricing_features && content.pricing_features.length > 0 ? content.pricing_features.map((f: any) => f.title) : [
                    "Full Access to All Modules",
                    "POS Billing + Inventory",
                    "CRM & Loyalty Programs",
                    "Accounting & Reports",
                    "Employee Management",
                    "Setup & Training Support",
                    "24/7 Customer Support",
                    "AI Photo Billing",
                  ]).map((feature, i) => (
                    <li key={i} className="flex items-start gap-3 text-sm text-foreground/80">
                      <svg
                        className="w-5 h-5 text-accent shrink-0 mt-0.5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Form Side */}
            <div className="bg-card shadow-lg rounded-2xl p-8 border border-border sticky top-24">
              <div className="mb-8">
                <h2 className="text-2xl font-bold text-foreground mb-2">Complete Your Purchase</h2>
                <p className="text-muted-foreground text-sm">Please fill in your details to proceed to checkout.</p>
              </div>

              <form onSubmit={handleSubmit} className="space-y-5">
                {/* Shop Name */}
                <div className="space-y-2">
                  <label className="text-sm font-medium text-foreground">
                    Shop / Business Name <span className="text-destructive">*</span>
                  </label>
                  <input
                    type="text"
                    name="shopName"
                    placeholder="e.g. Shyam General Store"
                    value={formData.shopName}
                    onChange={handleChange}
                    required
                    className="w-full border-2 border-border/50 rounded-xl p-3.5 bg-background focus:border-accent focus:ring-1 focus:ring-accent transition-colors"
                  />
                </div>

                {/* Owner Name */}
                <div className="space-y-2">
                  <label className="text-sm font-medium text-foreground">
                    Owner Full Name <span className="text-destructive">*</span>
                  </label>
                  <input
                    type="text"
                    name="ownerName"
                    placeholder="e.g. Ramesh Kumar"
                    value={formData.ownerName}
                    onChange={handleChange}
                    required
                    className="w-full border-2 border-border/50 rounded-xl p-3.5 bg-background focus:border-accent focus:ring-1 focus:ring-accent transition-colors"
                  />
                </div>

                {/* Mobile Number */}
                <div className="space-y-2">
                  <label className="text-sm font-medium text-foreground">
                    Mobile Number <span className="text-destructive">*</span>
                  </label>
                  <div className="flex">
                    <span className="inline-flex items-center px-4 rounded-l-xl border-2 border-r-0 border-border/50 bg-muted text-muted-foreground font-medium">
                      +91
                    </span>
                    <input
                      type="tel"
                      name="mobileNumber"
                      pattern="[0-9]{10}"
                      maxLength={10}
                      placeholder="9876543210"
                      value={formData.mobileNumber}
                      onChange={handleChange}
                      required
                      className="w-full border-2 border-border/50 rounded-r-xl p-3.5 bg-background focus:border-accent focus:ring-1 focus:ring-accent transition-colors"
                    />
                  </div>
                </div>

                {/* Referral Code */}
                <div className="space-y-2 pt-2">
                <label className="text-sm font-medium text-foreground">
                  Referral Code <span className="text-muted-foreground font-normal">(Optional)</span>
                </label>

                <div className="flex gap-2">
                  <input
                    type="text"
                    name="referralCode"
                    placeholder="Enter code if you have one"
                    value={formData.referralCode}
                    onChange={handleChange}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") {
                        e.preventDefault();
                        e.stopPropagation();
                        handleApplyReferral();
                      }
                    }}
                    className="flex-1 border-2 border-border/50 rounded-xl p-3.5 bg-background focus:border-accent focus:ring-1 focus:ring-accent transition-colors"
                  />

                  <button
                    type="button"
                    onClick={handleApplyReferral}
                    className="px-4 py-3 rounded-xl bg-accent text-white font-medium hover:opacity-90 transition"
                  >
                    Apply
                  </button>
                </div>
              </div>

                {/* Pay Button */}
                <div className="pt-4">
                  <Button
                    type="submit"
                    className="w-full bg-gold-gradient text-accent-foreground font-bold hover:shadow-lg hover:-translate-y-0.5 transition-all text-base py-6 rounded-xl"
                  >
                    Pay ₹{price.toLocaleString()} & Start Using AI-Setu
                  </Button>
                  <p className="text-xs text-center text-muted-foreground mt-4 flex items-center justify-center gap-1.5">
                    <svg
                      className="w-4 h-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                      />
                    </svg>
                    Secured by PhonePe
                  </p>
                </div>
              </form>
            </div>

          </div>
        </div>
      </div>

      <SolutionSection />
      <USPSection />
      <ComparisonSection />

      <Footer />
    </>
  );
};

export default PricingSignup;