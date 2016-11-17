
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
    "workspace_name",
    "read_library_ref"
})
public class FastqUtilsStatsParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("read_library_ref")
    private String readLibraryRef;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public FastqUtilsStatsParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("read_library_ref")
    public String getReadLibraryRef() {
        return readLibraryRef;
    }

    @JsonProperty("read_library_ref")
    public void setReadLibraryRef(String readLibraryRef) {
        this.readLibraryRef = readLibraryRef;
    }

    public FastqUtilsStatsParams withReadLibraryRef(String readLibraryRef) {
        this.readLibraryRef = readLibraryRef;
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
        return ((((((("FastqUtilsStatsParams"+" [workspaceName=")+ workspaceName)+", readLibraryRef=")+ readLibraryRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
