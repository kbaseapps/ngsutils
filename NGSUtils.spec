/*

*/
module NGSUtils {
    /* A string representing a ContigSet id. */
    typedef string read_library_name;

    /* A string representing a workspace name. */
    typedef string workspace_name;

    typedef structure {
        workspace_name workspace_name;
        read_library_name read_library_name;
    } FastqUtilsStatsParams;

    typedef structure {
        string report_name;
        string report_ref;
    } FastqUtilsStatsResult;
	
    funcdef fastqutils_stats(FastqUtilsStatsParams params) returns (FastqUtilsStatsResult) authentication required;
};