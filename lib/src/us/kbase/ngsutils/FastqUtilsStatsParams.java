
package us.kbase.ngsutils;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: FastqUtilsStatsParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace",
    "reads_library_name"
})
public class FastqUtilsStatsParams {

    @JsonProperty("workspace")
    private String workspace;
    @JsonProperty("reads_library_name")
    private String readsLibraryName;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace")
    public String getWorkspace() {
        return workspace;
    }

    @JsonProperty("workspace")
    public void setWorkspace(String workspace) {
        this.workspace = workspace;
    }

    public FastqUtilsStatsParams withWorkspace(String workspace) {
        this.workspace = workspace;
        return this;
    }

    @JsonProperty("reads_library_name")
    public String getReadsLibraryName() {
        return readsLibraryName;
    }

    @JsonProperty("reads_library_name")
    public void setReadsLibraryName(String readsLibraryName) {
        this.readsLibraryName = readsLibraryName;
    }

    public FastqUtilsStatsParams withReadsLibraryName(String readsLibraryName) {
        this.readsLibraryName = readsLibraryName;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((("FastqUtilsStatsParams"+" [workspace=")+ workspace)+", readsLibraryName=")+ readsLibraryName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
