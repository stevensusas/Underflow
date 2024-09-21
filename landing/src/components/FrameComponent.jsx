import PropTypes from "prop-types";
import styles from "./FrameComponent.module.css";

const FrameComponent = ({ className = "" }) => {
  return (
    <header className={[styles.frameParent, className].join(" ")}>
      <div className={styles.frameWrapper}>
        <div className={styles.frameGroup}>
          <div className={styles.materialSymbolsLightmoneyBWrapper}>
            <img
              className={styles.materialSymbolsLightmoneyBIcon}
              loading="lazy"
              alt=""
              src="/e53b7bd8-6b1d-4c5b-8020-1f62c0e8f5f9.png"
            />
          </div>
          <div className={styles.vectorWrapper}>
            <img
              className={styles.vectorIcon}
              loading="lazy"
              alt=""
              src="/vector.svg"
            />
          </div>
          <div className={styles.stackUnderflowWrapper}>
            <div className={styles.stackUnderflow}>Stack Underflow</div>
          </div>
        </div>
      </div>
      <div className={styles.frameContainer}>
        <div className={styles.logInParent}>
          <a className={styles.logIn}>Log in</a>
          <a className={styles.signUp}>Sign up</a>
        </div>
        <div className={styles.weuiarrowOutlinedWrapper}>
          <img
            className={styles.weuiarrowOutlinedIcon}
            loading="lazy"
            alt=""
            src="/33ab49db-761b-4ea5-b1e3-0f7494911488_1726936141625393326.png"
          />
        </div>
      </div>
    </header>
  );
};

FrameComponent.propTypes = {
  className: PropTypes.string,
};

export default FrameComponent;
