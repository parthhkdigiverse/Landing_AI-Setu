// import Header from "@/components/Header";
// import Footer from "@/components/Footer";
// import { motion } from "framer-motion";

// interface Props {
//   title: string;
//   location: string;
//   experience: string;
//   description: string[];
//   skills: string[];
// }

// const JobLayout = ({ title, location, experience, description, skills }: Props) => {
//   return (
//     <>
//       <Header />

//       <main className="bg-gray-50 py-20">

//         <div className="container mx-auto px-6 max-w-4xl">

//           <motion.h1
//             initial={{ opacity: 0, y: -30 }}
//             animate={{ opacity: 1, y: 0 }}
//             className="text-4xl font-bold mb-4"
//           >
//             {title}
//           </motion.h1>

//           <p className="text-gray-500 mb-10">
//             {experience} • {location}
//           </p>

//           <div className="bg-white p-10 rounded-xl shadow-lg space-y-8">

//             <div>
//               <h2 className="text-2xl font-semibold mb-4">
//                 Job Description
//               </h2>

//               <ul className="list-disc ml-6 space-y-2">
//                 {description.map((item, i) => (
//                   <li key={i}>{item}</li>
//                 ))}
//               </ul>
//             </div>

//             <div>
//               <h2 className="text-2xl font-semibold mb-4">
//                 Required Skills
//               </h2>

//               <ul className="flex flex-wrap gap-3">
//                 {skills.map((skill, i) => (
//                   <span
//                     key={i}
//                     className="bg-indigo-100 text-indigo-700 px-4 py-2 rounded-lg"
//                   >
//                     {skill}
//                   </span>
//                 ))}
//               </ul>
//             </div>

//             <button className="bg-indigo-600 text-white px-8 py-4 rounded-lg hover:bg-indigo-700">
//               Apply For This Job
//             </button>

//           </div>

//         </div>

//       </main>

//       <Footer />
//     </>
//   );
// };

// export default JobLayout;