import Header from "../components/common/Header";
import DocumentCard from "../components/team/DocumentCard";
import TeamInfoCard from "../components/team/TeamInfoCard";
import UserList from "../components/team/UserList";

const TeamPage: React.FC = () => {
  const team = {
    name: "Hemmalaget",
  };

  return (
    <div>
      <Header title="Hemmalaget" />
      <div className="grid grid-cols-1 gap-8 sm:grid-cols-3 sm:gap-4">
        <div className="col-span-2">
          <TeamInfoCard />
        </div>
        <div>
        <DocumentCard />
        </div>
      </div>
    <div className="py-4"><UserList /></div>
      
    </div>
  );
};

export default TeamPage;
