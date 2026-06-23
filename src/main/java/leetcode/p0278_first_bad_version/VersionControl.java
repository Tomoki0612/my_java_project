package leetcode.p0278_first_bad_version;

// Local stub of LeetCode's hidden parent class so the project compiles.
// Tests inject `bad` via Solution#firstBadVersion(int, int).
public class VersionControl {
    protected int bad;

    boolean isBadVersion(int version) {
        return version >= bad;
    }
}
