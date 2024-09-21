import FrameComponent from "./components/FrameComponent";
import FrameComponent1 from "./components/FrameComponent1";
import FrameComponent2 from "./components/FrameComponent2";
import styles from "./LandingPage.module.css";

const LandingPage = () => {
  return (
    <div className={styles.landingPage}>
      <FrameComponent />
      <FrameComponent1 />
      <FrameComponent2 />
      <div className={styles.landingPageChild} />
    </div>
  );
};

export default LandingPage;