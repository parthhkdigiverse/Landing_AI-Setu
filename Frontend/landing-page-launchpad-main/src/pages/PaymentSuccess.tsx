import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { CheckCircle2, Home, ArrowRight, ShieldCheck, Download, XCircle, Clock, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useNavigate, useSearchParams } from "react-router-dom";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

const PaymentSuccess = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const rawStatus = searchParams.get("status");
  const [status, setStatus] = useState(rawStatus?.toUpperCase() || "UNKNOWN");
  const tid = searchParams.get("tid") || "N/A";

  const [isPolling, setIsPolling] = useState(status === "PENDING" || status === "UNKNOWN");

  useEffect(() => {
    if (!isPolling || tid === "N/A") return;

    const pollInterval = setInterval(async () => {
      try {
        const response = await fetch(`/api/payment/status/${tid}/`);
        const data = await response.json();
        
        if (data.status === "SUCCESS" || data.status === "FAILURE") {
          setStatus(data.status);
          setIsPolling(false);
          clearInterval(pollInterval);
        }
      } catch (error) {
        console.error("Error polling payment status:", error);
      }
    }, 3000); // Poll every 3 seconds

    // Timeout after 1 minute
    const timeout = setTimeout(() => {
      setIsPolling(false);
      clearInterval(pollInterval);
    }, 60000);

    return () => {
      clearInterval(pollInterval);
      clearTimeout(timeout);
    };
  }, [isPolling, tid]);

  const renderContent = () => {
    // If we have no status at all in the URL, show a warning or loading
    if (!rawStatus) {
      return {
        icon: <Clock className="w-14 h-14 text-blue-600" />,
        iconBg: "bg-blue-100",
        title: "Verifying Payment",
        color: "text-blue-600",
        description: "Please wait while we confirm your transaction status with PhonePe.",
        accent: "bg-blue-400"
      };
    }

    switch (status) {
      case "SUCCESS":
        return {
          icon: <CheckCircle2 className="w-14 h-14 text-green-600" />,
          iconBg: "bg-green-100",
          title: "Payment Successful! 🎉",
          color: "text-green-600",
          description: (
            <>
              Welcome to <span className="font-bold text-[#F4B400]">AI-Setu ERP</span> family.  
              Your transaction has been completed successfully. You now have full access to our smart retail solutions.
            </>
          ),
          accent: "bg-gradient-to-r from-[#F4B400] via-[#FFD84D] to-[#E6B800]"
        };
      case "FAILURE":
        return {
          icon: <XCircle className="w-14 h-14 text-red-600" />,
          iconBg: "bg-red-100",
          title: "Payment Failed",
          color: "text-red-600",
          description: "Something went wrong with your transaction. Please check your bank details or try again after some time.",
          accent: "bg-red-500"
        };
      case "PENDING":
        return {
          icon: <Clock className="w-14 h-14 text-yellow-600" />,
          iconBg: "bg-yellow-100",
          title: "Payment Pending",
          color: "text-yellow-600",
          description: "Your payment is currently being processed by the bank. We will update your status as soon as we receive confirmation.",
          accent: "bg-yellow-400"
        };
      default:
        return {
          icon: <AlertCircle className="w-14 h-14 text-gray-600" />,
          iconBg: "bg-gray-100",
          title: `Status: ${status}`,
          color: "text-gray-600",
          description: "We've received a response from the payment gateway. Transaction ID: " + tid,
          accent: "bg-gray-400"
        };
    }
  };

  const content = renderContent();

  return (
    <>
      <Header />

      <main className="min-h-[80vh] flex items-center justify-center bg-gradient-to-b from-white to-[#F6F8FB] px-6 py-20">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="max-w-3xl w-full bg-white rounded-3xl shadow-xl border border-gray-100 p-10 md:p-14 text-center relative overflow-hidden"
        >
          {/* top gradient line */}
          <div className={`absolute top-0 left-0 w-full h-2 ${content.accent}`} />

          {/* status icon */}
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 180 }}
            className={`w-24 h-24 ${content.iconBg} rounded-full flex items-center justify-center mx-auto mb-8`}
          >
            {content.icon}
          </motion.div>

          {/* heading */}
          <h1 className="text-4xl md:text-5xl font-bold text-[#1F2E4D] mb-4">
            {content.title}
          </h1>

          {/* description */}
          <p className="text-lg text-gray-600 mb-12 leading-relaxed max-w-xl mx-auto">
            {content.description}
          </p>

          {/* transaction info */}
          <div className="bg-gray-50 rounded-xl p-3 mb-10 text-xs text-gray-500 inline-block px-6">
            Transaction ID: <span className="font-mono font-bold">{tid}</span>
          </div>

          {/* info cards (only for Success) */}
          {status === "SUCCESS" && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-12 text-left">
              <motion.div
                whileHover={{ y: -4 }}
                className="p-5 bg-blue-50 rounded-2xl flex items-start gap-3"
              >
                <ShieldCheck className="w-5 h-5 text-blue-600 mt-1" />
                <div>
                  <h3 className="font-semibold text-[#1F2E4D] text-sm">
                    Active Subscription
                  </h3>
                  <p className="text-xs text-gray-500">
                    Your account is now active and ready.
                  </p>
                </div>
              </motion.div>

              <motion.div
                whileHover={{ y: -4 }}
                className="p-5 bg-green-50 rounded-2xl flex items-start gap-3"
              >
                <Download className="w-5 h-5 text-green-600 mt-1" />
                <div>
                  <h3 className="font-semibold text-[#1F2E4D] text-sm">
                    Invoice Ready
                  </h3>
                  <p className="text-xs text-gray-500">
                    Download your receipt from our portal.
                  </p>
                </div>
              </motion.div>
            </div>
          )}

          {/* buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            {status !== "SUCCESS" ? (
              <Button
                onClick={() => navigate("/pricing-signup")}
                className="bg-[#F4B400] hover:bg-[#E6B800] text-white px-8 h-12 rounded-xl flex items-center gap-2"
              >
                Try Again
                <ArrowRight className="w-4 h-4" />
              </Button>
            ) : (
              <Button
                onClick={() => window.location.href = "https://aisetuerp.com/login"}
                className="bg-[#1F2E4D] hover:bg-[#2D3748] text-white px-8 h-12 rounded-xl flex items-center gap-2"
              >
                Go to Dashboard
                <ArrowRight className="w-4 h-4" />
              </Button>
            )}
            
            <Button
              onClick={() => navigate("/")}
              variant="outline"
              className="border-[#1F2E4D] text-[#1F2E4D] hover:bg-gray-50 px-8 h-12 rounded-xl flex items-center gap-2"
            >
              <Home className="w-4 h-4" />
              Back to Home
            </Button>
          </div>

          {/* small note */}
          <p className="text-xs text-gray-400 mt-8">
            {status === "SUCCESS" 
              ? "You will receive a confirmation email with your login details shortly."
              : "If you have any questions, please contact our support team."}
          </p>
        </motion.div>
      </main>

      <Footer />
    </>
  );
};

export default PaymentSuccess;
