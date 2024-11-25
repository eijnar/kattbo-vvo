import React from "react";
import ListUsers from "../components/users/ListUsers";
import { Heading } from "../components/catalyst/heading";

const LandingPage: React.FC = () => {
  return (
    <div>
      <div className="flex w-full flex-wrap items-end justify-between gap-4 border-b border-zinc-950/10 pb-6 dark:border-white/10">
        <Heading level={2}>Användare</Heading>
        <div className="flex gap-4"></div>
      </div>
      <ListUsers />
    </div>
  );
};

export default LandingPage;
