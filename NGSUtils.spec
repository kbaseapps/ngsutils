/*

*/
module NGSUtils {
    /* A string representing a ContigSet id. */
    typedef string read_library_ref;

    /* A string representing a workspace name. */
    typedef string workspace_name;

    typedef structure {
        workspace_name workspace_name;
        read_library_ref read_library_ref;
    } FastqUtilsStatsParams;

    typedef structure {
        string report_name;
        string report_ref;
    } FastqUtilsStatsResult;
	
    funcdef fastqutils_stats(FastqUtilsStatsParams params) returns (FastqUtilsStatsResult) authentication required;
};